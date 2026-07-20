<script lang="ts">
	import type { CurrentReading, SensorStatus } from '$lib/types';
	import { formatSensorAge } from '$lib/format';

	let {
		location,
		status,
		reading
	}: {
		location: string;
		status?: SensorStatus;
		reading?: CurrentReading;
	} = $props();
</script>

<section class="reading-card" class:green={status?.status === 'Green'} class:yellow={status?.status === 'Yellow'} class:red={status?.status === 'Red'}>
	<h2>Current — {location}</h2>
	{#if status}
		<p class="status-line">
			Status: <strong>{status.status}</strong> · last reading {formatSensorAge(status.diff_seconds)} ago
		</p>
	{/if}
	{#if reading}
		<div class="metrics">
			<div class="metric">
				<span class="label">Temperature</span>
				<span class="value">{reading.temperature_f}°F</span>
			</div>
			<div class="metric">
				<span class="label">Heat Index</span>
				<span class="value">{reading.heat_index_f}°F</span>
			</div>
			<div class="metric">
				<span class="label">Humidity</span>
				<span class="value">{reading.humidity_pct}%</span>
			</div>
			<div class="metric">
				<span class="label">Pressure</span>
				<span class="value">{reading.pressure_inHg} inHg</span>
			</div>
		</div>
	{:else}
		<p class="empty">No reading available for this location.</p>
	{/if}
</section>

<style>
	.reading-card {
		padding: 1rem 1.25rem;
		border-radius: 10px;
		border: 2px solid #444;
		background: #1a1a1a;
		margin-bottom: 1.5rem;
	}

	.status-line {
		margin: 0 0 1rem;
		color: #aaa;
		font-size: 0.9rem;
	}

	.metrics {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: 1rem;
	}

	.metric {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.label {
		font-size: 0.8rem;
		color: #888;
		text-transform: uppercase;
		letter-spacing: 0.03em;
	}

	.value {
		font-size: 1.35rem;
		font-weight: 600;
	}

	.empty {
		color: #888;
		margin: 0;
	}

	.green {
		border-color: #4caf50;
	}

	.yellow {
		border-color: #ffeb3b;
	}

	.red {
		border-color: #ef5350;
	}
</style>
