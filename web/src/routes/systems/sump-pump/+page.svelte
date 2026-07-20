<script lang="ts">
	import { onMount } from 'svelte';
	import { getSumpPumpCharts, getSumpPumpCycles } from '$lib/api';
	import { buildBarChart, buildSingleSeriesChart } from '$lib/charts';
	import type { ChartDataset } from '$lib/charts';
	import { REFRESH_MS } from '$lib/constants';
	import type { SumpCycleRow } from '$lib/types';
	import ChartPanel from '$lib/components/ChartPanel.svelte';
	import DashboardShell from '$lib/components/DashboardShell.svelte';

	let sumpChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let sumpCycleChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let error = $state<string | null>(null);
	let lastUpdated = $state<Date | null>(null);
	let loading = $state(true);

	async function refresh() {
		try {
			const [sumpRows, sumpCycles] = await Promise.all([getSumpPumpCharts(), getSumpPumpCycles()]);

			sumpChart = buildSingleSeriesChart(
				sumpRows.map((r) => ({
					reading_dttm: r.reading_dttm,
					value: parseFloat(String(r.water_level))
				})),
				'Water Level',
				'#4fc3f7'
			);

			sumpCycleChart = buildBarChart(
				(sumpCycles as SumpCycleRow[]).map((r) => ({
					label: r.reading_date,
					value: parseInt(r.num_cycles, 10)
				})),
				'Cycles',
				'#81c784'
			);

			error = null;
			lastUpdated = new Date();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load sump pump data';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		refresh();
		const id = setInterval(refresh, REFRESH_MS);
		return () => clearInterval(id);
	});
</script>

<DashboardShell title="Sump Pump" {error} {loading} {lastUpdated} onRefresh={refresh}>
	<ChartPanel title="Water Level (24 hours)" labels={sumpChart.labels} datasets={sumpChart.datasets} />
	<ChartPanel
		title="Cycles per Day"
		labels={sumpCycleChart.labels}
		datasets={sumpCycleChart.datasets}
		type="bar"
	/>
</DashboardShell>
