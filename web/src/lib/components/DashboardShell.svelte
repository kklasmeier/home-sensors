<script lang="ts">
	import type { Snippet } from 'svelte';
	import { REFRESH_MS } from '$lib/constants';

	let {
		title,
		error = null,
		loading = false,
		lastUpdated = null,
		onRefresh,
		children
	}: {
		title: string;
		error?: string | null;
		loading?: boolean;
		lastUpdated?: Date | null;
		onRefresh: () => void | Promise<void>;
		children: Snippet;
	} = $props();
</script>

<div class="dashboard">
	<header class="page-header">
		<h1>{title}</h1>

		<div class="toolbar">
			<div class="meta">
				{#if loading}
					Loading…
				{:else if lastUpdated}
					Updated {lastUpdated.toLocaleTimeString()} · auto-refresh every {REFRESH_MS / 1000}s
				{/if}
			</div>
			<button type="button" onclick={() => onRefresh()}>Refresh now</button>
		</div>
	</header>

	{#if error}
		<div class="error-banner">{error}</div>
	{/if}

	{@render children()}
</div>

<style>
	.page-header {
		margin-bottom: 1rem;
	}

	h1 {
		margin: 0.5rem 0;
		text-align: left;
	}

	.dashboard {
		padding: 0;
		max-width: none;
		margin: 0;
	}
</style>
