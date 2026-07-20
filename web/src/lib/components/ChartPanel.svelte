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

	let canvas = $state<HTMLCanvasElement | null>(null);
	let chart: Chart | null = null;

	function render() {
		if (!canvas) return;
		chart?.destroy();

		const config: ChartConfiguration = {
			type,
			data: {
				labels,
				datasets: datasets.map((d) => ({
					label: d.label,
					data: d.data,
					borderColor: d.borderColor,
					backgroundColor: type === 'bar' ? `${d.borderColor}99` : 'transparent',
					tension: 0.1,
					spanGaps: true,
					stepped: type === 'line' && d.label.includes('Door') ? ('before' as const) : false
				}))
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: { labels: { color: '#e0e0e0' } },
					title: { display: true, text: title, color: '#ffffff', font: { size: 16 } }
				},
				scales: {
					x: {
						ticks: { color: '#9e9e9e', maxRotation: 45, autoSkip: true, maxTicksLimit: 12 },
						grid: { color: '#333' }
					},
					y: {
						ticks: { color: '#9e9e9e' },
						grid: { color: '#333' },
						beginAtZero: type === 'bar'
					}
				}
			}
		};

		chart = new Chart(canvas, config);
	}

	$effect(() => {
		labels;
		datasets;
		title;
		type;
		render();
		return () => {
			chart?.destroy();
			chart = null;
		};
	});
</script>

<div class="chart-panel" style="height: {height}px">
	<canvas bind:this={canvas}></canvas>
</div>

<style>
	.chart-panel {
		position: relative;
		width: 100%;
		margin-bottom: 1.5rem;
	}
</style>
