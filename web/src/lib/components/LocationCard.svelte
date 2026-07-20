<script lang="ts">
	import { locationPath } from '$lib/constants';
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

<a class="nav-card" class:green={status?.status === 'Green'} class:yellow={status?.status === 'Yellow'} class:red={status?.status === 'Red'} href={locationPath(location)}>
	<h3>{location}</h3>
	<p class="age">{status ? formatSensorAge(status.diff_seconds) : '—'} since last reading</p>
	{#if reading}
		<p class="reading">{reading.temperature_f}°F · {reading.humidity_pct}% RH</p>
	{:else}
		<p class="reading muted">No current reading</p>
	{/if}
	<span class="cta">View charts &amp; history →</span>
</a>

<style>
	.nav-card {
		display: block;
		padding: 1rem 1.25rem;
		border-radius: 10px;
		border: 2px solid #444;
		background: #1e1e1e;
		color: inherit;
		text-decoration: none;
		transition: border-color 0.15s, transform 0.15s;
	}

	.nav-card:hover {
		border-color: #666;
		transform: translateY(-2px);
	}

	.nav-card h3 {
		margin: 0 0 0.35rem;
		font-size: 1.15rem;
	}

	.age {
		margin: 0;
		font-size: 0.85rem;
		color: #aaa;
	}

	.reading {
		margin: 0.5rem 0;
		font-weight: 600;
	}

	.muted {
		color: #888;
		font-weight: 400;
	}

	.cta {
		font-size: 0.8rem;
		color: #4fc3f7;
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
