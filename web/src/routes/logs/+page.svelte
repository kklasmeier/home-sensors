<script lang="ts">
	import { onMount } from 'svelte';
	import { getCollectLogs } from '$lib/api';
	import { REFRESH_MS } from '$lib/constants';
	import DashboardShell from '$lib/components/DashboardShell.svelte';

	let content = $state('');
	let error = $state<string | null>(null);
	let lastUpdated = $state<Date | null>(null);
	let loading = $state(true);
	let logEl = $state<HTMLPreElement | null>(null);

	async function refresh() {
		try {
			const lines = (await getCollectLogs()).trim().split('\n');
			content = lines.slice(-2000).join('\n');
			error = null;
			lastUpdated = new Date();
			requestAnimationFrame(() => {
				if (logEl) logEl.scrollTop = logEl.scrollHeight;
			});
		} catch (e) {
			error = e instanceof Error ? e.message : 'Could not load log file';
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

<DashboardShell title="Collector Logs" {error} {loading} {lastUpdated} onRefresh={refresh}>
	<p class="hint">Last 2000 lines from <code>collect_data.log</code>. Auto-refreshes with the rest of the dashboard.</p>
	<pre bind:this={logEl} class="log-view"><code>{content || (loading ? 'Loading…' : '')}</code></pre>
</DashboardShell>

<style>
	.hint {
		margin: 0 0 1rem;
		color: #888;
		font-size: 0.9rem;
	}

	code {
		color: #c5e1a5;
	}

	.log-view {
		margin: 0;
		padding: 1rem;
		overflow: auto;
		max-height: calc(100vh - 280px);
		min-height: 320px;
		font-size: 0.8rem;
		line-height: 1.4;
		background: #121212;
		border: 1px solid #333;
		border-radius: 8px;
	}

	.log-view code {
		white-space: pre-wrap;
		word-break: break-word;
	}
</style>
