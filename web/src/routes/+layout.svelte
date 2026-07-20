<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import Breadcrumbs from '$lib/components/Breadcrumbs.svelte';
	import { breadcrumbsForPath } from '$lib/navigation';

	let { children } = $props();

	const crumbs = $derived(breadcrumbsForPath($page.url.pathname));
	const isHome = $derived($page.url.pathname === '/' || $page.url.pathname === '');
</script>

<svelte:head>
	<title>Home Sensor Dashboard</title>
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<div class="app-shell">
	<header class="site-header">
		<a class="site-home" href="/">Home Sensor Dashboard</a>
		<nav class="site-nav" aria-label="Site">
			<a href="/logs" class:active={$page.url.pathname === '/logs'}>Logs</a>
		</nav>
		{#if !isHome}
			<a class="back-button" href="/">← Back to overview</a>
		{/if}
	</header>

	<div class="page-body">
		<Breadcrumbs {crumbs} />
		{@render children()}
	</div>
</div>

<style>
	.app-shell {
		min-height: 100vh;
	}

	.site-header {
		display: grid;
		grid-template-columns: 1fr auto auto;
		align-items: center;
		gap: 0.75rem 1rem;
		padding: 0.75rem 1rem;
		background: #1a1a1a;
		border-bottom: 1px solid #333;
	}

	@media (max-width: 640px) {
		.site-header {
			grid-template-columns: 1fr auto;
		}

		.back-button {
			grid-column: 1 / -1;
			justify-self: start;
		}
	}

	.site-nav {
		display: flex;
		gap: 0.75rem;
	}

	.site-nav a {
		color: #aaa;
		text-decoration: none;
		font-size: 0.9rem;
	}

	.site-nav a:hover,
	.site-nav a.active {
		color: #4fc3f7;
	}

	.site-home {
		color: #e0e0e0;
		font-weight: 700;
		font-size: 1.05rem;
		text-decoration: none;
	}

	.site-home:hover {
		color: #4fc3f7;
	}

	.back-button {
		color: #4fc3f7;
		text-decoration: none;
		font-size: 0.9rem;
		white-space: nowrap;
	}

	.back-button:hover {
		text-decoration: underline;
	}

	.page-body {
		max-width: 1400px;
		margin: 0 auto;
		padding: 0 1rem 2rem;
	}
</style>
