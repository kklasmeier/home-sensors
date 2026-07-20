<script lang="ts">
	import { Chart, registerables, type ChartConfiguration } from 'chart.js';
	import type { ChartDataset } from '$lib/charts';

	Chart.register(...registerables);

	let {
		title,
		labels,
		datasets,
		type = 'line',
		height = 300
	}: {
		title: string;
		labels: string[];
		datasets: ChartDataset[];
		type?: 'line' | 'bar';
		height?: number;
	} = $props();

	type ChartParams = {
		title: string;
		labels: string[];
		datasets: ChartDataset[];
		type: 'line' | 'bar';
	};

	/** Chart.js mutates config data; must not pass Svelte reactive proxies. */
	function plainParams(params: ChartParams): ChartParams {
		const snap = $state.snapshot(params);
		return {
			title: snap.title,
			type: snap.type,
			labels: [...snap.labels],
			datasets: snap.datasets.map((d) => ({
				label: d.label,
				borderColor: d.borderColor,
				data: [...d.data]
			}))
		};
	}

	function makeConfig(params: ChartParams): ChartConfiguration {
		const plain = plainParams(params);
		return {
			type: plain.type,
			data: {
				labels: plain.labels,
				datasets: plain.datasets.map((d) => ({
					label: d.label,
					data: d.data,
					borderColor: d.borderColor,
					backgroundColor: plain.type === 'bar' ? `${d.borderColor}99` : 'transparent',
					tension: 0.1,
					spanGaps: true,
					...(plain.type === 'line' && d.label.includes('Door')
						? { stepped: 'before' as const }
						: {})
				}))
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				animation: false,
				plugins: {
					legend: { labels: { color: '#e0e0e0' } },
					title: {
						display: true,
						text: plain.title,
						color: '#ffffff',
						font: { size: 16 }
					}
				},
				scales: {
					x: {
						ticks: { color: '#9e9e9e', maxRotation: 45, autoSkip: true, maxTicksLimit: 12 },
						grid: { color: '#333' }
					},
					y: {
						ticks: { color: '#9e9e9e' },
						grid: { color: '#333' },
						beginAtZero: plain.type === 'bar'
					}
				}
			}
		};
	}

	function chartAction(canvas: HTMLCanvasElement, params: ChartParams) {
		let chart = new Chart(canvas, makeConfig(params));
		return {
			update(newParams: ChartParams) {
				chart.destroy();
				chart = new Chart(canvas, makeConfig(newParams));
			},
			destroy() {
				chart.destroy();
			}
		};
	}

	const chartParams = $derived({ title, labels, datasets, type });
</script>

<div class="chart-panel" style="height: {height}px">
	<canvas use:chartAction={chartParams}></canvas>
</div>

<style>
	.chart-panel {
		position: relative;
		width: 100%;
		margin-bottom: 1.5rem;
	}

	.empty {
		color: #888;
		text-align: center;
		padding: 2rem;
	}
</style>
