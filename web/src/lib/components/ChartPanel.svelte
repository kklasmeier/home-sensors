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

	function makeConfig(params: ChartParams): ChartConfiguration {
		return {
			type: params.type,
			data: {
				labels: params.labels,
				datasets: params.datasets.map((d) => ({
					label: d.label,
					data: d.data,
					borderColor: d.borderColor,
					backgroundColor: params.type === 'bar' ? `${d.borderColor}99` : 'transparent',
					tension: 0.1,
					spanGaps: true,
					...(params.type === 'line' && d.label.includes('Door')
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
						text: params.title,
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
						beginAtZero: params.type === 'bar'
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
	const hasData = $derived(datasets.some((d) => d.data.some((v) => v !== null)));
</script>

<div class="chart-panel" style="height: {height}px">
	{#if hasData}
		<canvas use:chartAction={chartParams}></canvas>
	{:else}
		<p class="empty">No data for this period</p>
	{/if}
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
