<script lang="ts">
	import { onMount } from 'svelte';
	import {
		getAllLocationCharts,
		getAllSummaries,
		getCollectLogs,
		getCurrentReadings,
		getGarageCharts,
		getGarageStatus,
		getHvacCycles,
		getSensorStatus,
		getSumpPumpCharts,
		getSumpPumpCycles
	} from '$lib/api';
	import { buildBarChart, buildMultiLocationChart, buildSingleSeriesChart } from '$lib/charts';
	import type { ChartDataset } from '$lib/charts';
	import { REFRESH_MS } from '$lib/constants';
	import { formatChartLabel } from '$lib/format';
	import type {
		CurrentReadings,
		GarageChartRow,
		GarageDoor,
		HvacCycleRow,
		SensorStatus,
		SummaryData,
		SumpCycleRow
	} from '$lib/types';
	import ChartPanel from '$lib/components/ChartPanel.svelte';
	import CurrentReadingsTable from '$lib/components/CurrentReadingsTable.svelte';
	import GaragePanel from '$lib/components/GaragePanel.svelte';
	import LogModal from '$lib/components/LogModal.svelte';
	import SensorGrid from '$lib/components/SensorGrid.svelte';
	import SummaryTables from '$lib/components/SummaryTables.svelte';

	let statuses = $state<SensorStatus[]>([]);
	let readings = $state<CurrentReadings>({});
	let doors = $state<GarageDoor[]>([]);
	let summaries = $state<Record<string, SummaryData>>({});
	let logOpen = $state(false);
	let logContent = $state('');
	let error = $state<string | null>(null);
	let lastUpdated = $state<Date | null>(null);
	let loading = $state(true);

	let tempChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let heatChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let humidityChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let pressureChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let sumpChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let sumpCycleChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let hvacCycleChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });
	let garageChart = $state({ labels: [] as string[], datasets: [] as ChartDataset[] });

	function buildGarageDoorChart(rows: GarageChartRow[]) {
		return {
			labels: rows.map((r) => formatChartLabel(r.reading_dttm)),
			datasets: [
				{
					label: 'Main Garage Door',
					borderColor: '#4fc3f7',
					data: rows.map((r) => r.mainGarageDoor)
				},
				{
					label: '3rd Car Door',
					borderColor: '#ffb74d',
					data: rows.map((r) => r.thirdCarDoor)
				}
			]
		};
	}

	async function refresh() {
		try {
			const [
				statusData,
				currentData,
				garageStatus,
				chartRows,
				garageRows,
				sumpRows,
				sumpCycles,
				hvacCycles,
				summaryData
			] = await Promise.all([
				getSensorStatus(),
				getCurrentReadings(),
				getGarageStatus(),
				getAllLocationCharts(),
				getGarageCharts(),
				getSumpPumpCharts(),
				getSumpPumpCycles(),
				getHvacCycles(),
				getAllSummaries()
			]);

			statuses = statusData;
			readings = currentData;
			doors = garageStatus.doors;
			summaries = summaryData;

			tempChart = buildMultiLocationChart(chartRows, 'temperature_f');
			heatChart = buildMultiLocationChart(chartRows, 'heat_index_f');
			humidityChart = buildMultiLocationChart(chartRows, 'humidity_pct');
			pressureChart = buildMultiLocationChart(chartRows, 'pressure_inHg');

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

			hvacCycleChart = buildBarChart(
				(hvacCycles as HvacCycleRow[]).map((r) => ({
					label: r.cycle_date,
					value: r.cycle_count
				})),
				'Cycles',
				'#f06292'
			);

			garageChart = buildGarageDoorChart(garageRows);

			error = null;
			lastUpdated = new Date();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load dashboard';
		} finally {
			loading = false;
		}
	}

	async function showLogs() {
		try {
			const lines = (await getCollectLogs()).trim().split('\n');
			logContent = lines.slice(-2000).join('\n');
			logOpen = true;
		} catch {
			error = 'Could not load log file';
		}
	}

	onMount(() => {
		refresh();
		const id = setInterval(refresh, REFRESH_MS);
		return () => clearInterval(id);
	});
</script>

<div class="dashboard">
	<h1>Home Sensor Dashboard</h1>

	<div class="toolbar">
		<button type="button" onclick={showLogs}>Show Logs</button>
		<div class="meta">
			{#if loading}
				Loading…
			{:else if lastUpdated}
				Updated {lastUpdated.toLocaleTimeString()} · auto-refresh every {REFRESH_MS / 1000}s
			{/if}
		</div>
		<button type="button" onclick={refresh}>Refresh now</button>
	</div>

	{#if error}
		<div class="error-banner">{error}</div>
	{/if}

	<SensorGrid {statuses} />
	<GaragePanel {doors} />
	<CurrentReadingsTable {readings} />

	<ChartPanel title="Temperature over time" labels={tempChart.labels} datasets={tempChart.datasets} />
	<ChartPanel title="Heat Index over time" labels={heatChart.labels} datasets={heatChart.datasets} />
	<ChartPanel title="Humidity over time" labels={humidityChart.labels} datasets={humidityChart.datasets} />
	<ChartPanel title="Pressure over time" labels={pressureChart.labels} datasets={pressureChart.datasets} />
	<ChartPanel title="Sump Pump Water Level" labels={sumpChart.labels} datasets={sumpChart.datasets} />
	<ChartPanel
		title="Number of Sump Pump Cycles per Day"
		labels={sumpCycleChart.labels}
		datasets={sumpCycleChart.datasets}
		type="bar"
	/>
	<ChartPanel
		title="Number of HVAC Cycles per Day"
		labels={hvacCycleChart.labels}
		datasets={hvacCycleChart.datasets}
		type="bar"
		height={400}
	/>
	<ChartPanel
		title="Garage Door History"
		labels={garageChart.labels}
		datasets={garageChart.datasets}
	/>

	<SummaryTables {summaries} />
</div>

<LogModal bind:open={logOpen} content={logContent} />
