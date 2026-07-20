<script lang="ts">
	import { onMount } from 'svelte';
	import { getCurrentReadings, getGarageStatus, getSensorStatus } from '$lib/api';
	import { ENV_LOCATIONS, REFRESH_MS, SYSTEM_ROUTES } from '$lib/constants';
	import type { CurrentReadings, GarageDoor, SensorStatus } from '$lib/types';
	import DashboardShell from '$lib/components/DashboardShell.svelte';
	import GaragePanel from '$lib/components/GaragePanel.svelte';
	import LocationCard from '$lib/components/LocationCard.svelte';
	import CurrentReadingsTable from '$lib/components/CurrentReadingsTable.svelte';
	import SensorGrid from '$lib/components/SensorGrid.svelte';
	import SystemCard from '$lib/components/SystemCard.svelte';

	let statuses = $state<SensorStatus[]>([]);
	let readings = $state<CurrentReadings>({});
	let doors = $state<GarageDoor[]>([]);
	let error = $state<string | null>(null);
	let lastUpdated = $state<Date | null>(null);
	let loading = $state(true);

	const statusMap = $derived(Object.fromEntries(statuses.map((s) => [s.location, s])));

	function garageSummary(doorList: GarageDoor[]): string {
		if (!doorList.length) return 'No door data';
		return doorList.map((d) => `${d.label.replace(' Door', '')}: ${d.status}`).join(' · ');
	}

	async function refresh() {
		try {
			const [statusData, currentData, garageStatus] = await Promise.all([
				getSensorStatus(),
				getCurrentReadings(),
				getGarageStatus()
			]);
			statuses = statusData;
			readings = currentData;
			doors = garageStatus.doors;
			error = null;
			lastUpdated = new Date();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load dashboard';
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

<DashboardShell title="Home Sensor Dashboard" {error} {loading} {lastUpdated} onRefresh={refresh}>
	<SensorGrid {statuses} />
	<GaragePanel {doors} />
	<CurrentReadingsTable {readings} />

	<section class="section" id="locations">
		<h2>Locations</h2>
		<p class="section-hint">Open a location for 24-hour charts and high/low summaries.</p>
		<div class="card-grid">
			{#each ENV_LOCATIONS as location (location)}
				<LocationCard
					{location}
					status={statusMap[location]}
					reading={readings[location] ?? null}
				/>
			{/each}
		</div>
	</section>

	<section class="section" id="systems">
		<h2>Systems</h2>
		<p class="section-hint">Garage doors, sump pump, and HVAC cycle history.</p>
		<div class="card-grid">
			{#each SYSTEM_ROUTES as system (system.slug)}
				<SystemCard
					slug={system.slug}
					label={system.label}
					status={statusMap[system.statusKey]}
					summary={system.slug === 'garage-doors' ? garageSummary(doors) : undefined}
				/>
			{/each}
		</div>
	</section>
</DashboardShell>

<style>
	.section {
		margin-top: 2rem;
	}

	.section h2 {
		margin-bottom: 0.25rem;
	}

	.section-hint {
		margin: 0 0 1rem;
		color: #888;
		font-size: 0.9rem;
	}

	.card-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 1rem;
	}
</style>
