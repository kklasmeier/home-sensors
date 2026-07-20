<script lang="ts">
	import { systemPath } from '$lib/constants';
	import type { SensorStatus } from '$lib/types';
	import { displayLocationName, formatSensorAge } from '$lib/format';

	let {
		slug,
		label,
		status,
		summary
	}: {
		slug: string;
		label: string;
		status?: SensorStatus;
		summary?: string;
	} = $props();
</script>

<a
	class="nav-card system"
	class:green={status?.status === 'Green'}
	class:yellow={status?.status === 'Yellow'}
	class:red={status?.status === 'Red'}
	href={systemPath(slug)}
>
	<h3>{label}</h3>
	{#if status}
		<p class="age">{displayLocationName(status.location)}: {formatSensorAge(status.diff_seconds)} ago</p>
	{/if}
	{#if summary}
		<p class="summary">{summary}</p>
	{/if}
	<span class="cta">View details →</span>
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

	.summary {
		margin: 0.5rem 0;
		font-weight: 600;
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
