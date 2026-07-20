<script lang="ts">
	import { onMount } from 'svelte';
	import { getGarageCharts, getGarageStatus } from '$lib/api';
	import { buildGarageDoorChart } from '$lib/charts';
	import type { ChartDataset } from '$lib/charts';
	import { REFRESH_MS } from '$lib/constants';
	import type { GarageDoor } from '$lib/types';
	import ChartPanel from '$lib/components/ChartPanel.svelte';
	import DashboardShell from '$lib/components/DashboardShell.svelte';
	import GaragePanel from '$lib/components/GaragePanel.svelte';

	let doors = $state<GarageDoor[]>([]);
	let garageChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let error = $state<string | null>(null);
	let lastUpdated = $state<Date | null>(null);
	let loading = $state(true);

	async function refresh() {
		try {
			const [garageStatus, garageRows] = await Promise.all([getGarageStatus(), getGarageCharts()]);
			doors = garageStatus.doors;
			garageChart = buildGarageDoorChart(garageRows);
			error = null;
			lastUpdated = new Date();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load garage doors';
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

<DashboardShell title="Garage Doors" {error} {loading} {lastUpdated} onRefresh={refresh}>
	<GaragePanel {doors} />
	<ChartPanel title="Garage Door History (24 hours)" labels={garageChart.labels} datasets={garageChart.datasets} />
</DashboardShell>
