<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import {
		getCurrentReadings,
		getLocationCharts,
		getLocationSummary,
		getSensorStatus
	} from '$lib/api';
	import { buildLocationChartSet } from '$lib/charts';
	import type { ChartDataset } from '$lib/charts';
	import { CHART_COLORS, isEnvLocation, REFRESH_MS } from '$lib/constants';
	import type { CurrentReading, SensorStatus, SummaryData } from '$lib/types';
	import ChartPanel from '$lib/components/ChartPanel.svelte';
	import DashboardShell from '$lib/components/DashboardShell.svelte';
	import LocationReadingCard from '$lib/components/LocationReadingCard.svelte';
	import SummaryTable from '$lib/components/SummaryTable.svelte';

	const location = $derived(decodeURIComponent($page.params.location ?? ''));

	let status = $state<SensorStatus | undefined>();
	let reading = $state<CurrentReading | undefined>();
	let summary = $state<SummaryData | null>(null);
	let tempChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let heatChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let humidityChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let pressureChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let error = $state<string | null>(null);
	let lastUpdated = $state<Date | null>(null);
	let loading = $state(true);

	async function refresh() {
		if (!isEnvLocation(location)) {
			error = `Unknown location: ${location}`;
			loading = false;
			return;
		}

		try {
			const [statusData, currentData, chartRows, summaryData] = await Promise.all([
				getSensorStatus(),
				getCurrentReadings(),
				getLocationCharts(location),
				getLocationSummary(location)
			]);

			status = statusData.find((s) => s.location === location);
			reading = currentData[location] ?? null;
			summary = summaryData;

			const color = CHART_COLORS[location] ?? '#4fc3f7';
			const charts = buildLocationChartSet(chartRows, location, color);
			tempChart = charts.temperature;
			heatChart = charts.heatIndex;
			humidityChart = charts.humidity;
			pressureChart = charts.pressure;

			error = null;
			lastUpdated = new Date();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load location';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		const id = setInterval(refresh, REFRESH_MS);
		return () => clearInterval(id);
	});

	$effect(() => {
		location;
		loading = true;
		refresh();
	});
</script>

<DashboardShell title={location} {error} {loading} {lastUpdated} onRefresh={refresh}>
	<LocationReadingCard {location} {status} {reading} />

	<h2>Last 24 hours</h2>
	<ChartPanel title="Temperature" labels={tempChart.labels} datasets={tempChart.datasets} />
	<ChartPanel title="Heat Index" labels={heatChart.labels} datasets={heatChart.datasets} />
	<ChartPanel title="Humidity" labels={humidityChart.labels} datasets={humidityChart.datasets} />
	<ChartPanel title="Pressure" labels={pressureChart.labels} datasets={pressureChart.datasets} />

	{#if summary}
		<SummaryTable {location} data={summary} />
	{/if}
</DashboardShell>
