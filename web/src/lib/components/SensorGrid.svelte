<script lang="ts">
	import type { SensorStatus } from '$lib/types';
	import { displayLocationName, formatSensorAge } from '$lib/format';

	let { statuses }: { statuses: SensorStatus[] } = $props();

	const statusMap = $derived(
		Object.fromEntries(statuses.map((s) => [s.location, s])) as Record<string, SensorStatus>
	);
</script>

<div class="sensor-grid">
	{#each ['Attic', 'Garage', 'Inside', 'Outside', 'Garagedoor', 'SumpPump', 'HVAC'] as location (location)}
		{@const sensor = statusMap[location]}
		<div
			class="sensor-tile"
			class:green={sensor?.status === 'Green'}
			class:yellow={sensor?.status === 'Yellow'}
			class:red={sensor?.status === 'Red'}
			class:unknown={!sensor}
		>
			{displayLocationName(location)}:
			{sensor ? formatSensorAge(sensor.diff_seconds) : '—'}
		</div>
	{/each}
</div>

<style>
	.sensor-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: 0.75rem;
		margin-bottom: 1.5rem;
	}

	.sensor-tile {
		padding: 1rem;
		border-radius: 8px;
		text-align: center;
		font-weight: 600;
		background: #2a2a2a;
		border: 2px solid #444;
	}

	.green {
		background: #1b5e20;
		border-color: #4caf50;
	}

	.yellow {
		background: #f57f17;
		border-color: #ffeb3b;
		color: #111;
	}

	.red {
		background: #b71c1c;
		border-color: #ef5350;
	}

	.unknown {
		background: #424242;
		border-color: #757575;
	}
</style>
