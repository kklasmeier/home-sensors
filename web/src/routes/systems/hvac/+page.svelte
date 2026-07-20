<script lang="ts">
	import { onMount } from 'svelte';
	import { getHvacCycles } from '$lib/api';
	import { buildBarChart } from '$lib/charts';
	import type { ChartDataset } from '$lib/charts';
	import { locationPath, REFRESH_MS } from '$lib/constants';
	import type { HvacCycleRow } from '$lib/types';
	import ChartPanel from '$lib/components/ChartPanel.svelte';
	import DashboardShell from '$lib/components/DashboardShell.svelte';

	let hvacCycleChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let error = $state<string | null>(null);
	let lastUpdated = $state<Date | null>(null);
	let loading = $state(true);

	async function refresh() {
		try {
			const hvacCycles = await getHvacCycles();

			hvacCycleChart = buildBarChart(
				(hvacCycles as HvacCycleRow[]).map((r) => ({
					label: r.cycle_date,
					value: r.cycle_count
				})),
				'Cycles',
				'#f06292'
			);

			error = null;
			lastUpdated = new Date();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load HVAC cycles';
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

<DashboardShell title="HVAC Cycles" {error} {loading} {lastUpdated} onRefresh={refresh}>
	<p class="hint">
		For temperature and humidity at the HVAC sensor, see
		<a href={locationPath('HVAC')}>HVAC location</a>.
	</p>
	<ChartPanel
		title="Cycles per Day"
		labels={hvacCycleChart.labels}
		datasets={hvacCycleChart.datasets}
		type="bar"
		height={400}
	/>
</DashboardShell>

<style>
	.hint {
		color: #888;
		margin: 0 0 1rem;
		font-size: 0.9rem;
	}

	a {
		color: #4fc3f7;
	}
</style>
