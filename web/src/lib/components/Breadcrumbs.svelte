<script lang="ts">
	import type { Breadcrumb } from '$lib/navigation';

	let { crumbs }: { crumbs: Breadcrumb[] } = $props();
</script>

<nav class="breadcrumbs" aria-label="Breadcrumb">
	<ol>
		{#each crumbs as crumb, index (crumb.label + index)}
			<li>
				{#if crumb.href && index < crumbs.length - 1}
					<a href={crumb.href}>{crumb.label}</a>
				{:else}
					<span aria-current="page">{crumb.label}</span>
				{/if}
			</li>
		{/each}
	</ol>
</nav>

<style>
	.breadcrumbs {
		margin-bottom: 0.75rem;
	}

	ol {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.35rem;
		list-style: none;
		margin: 0;
		padding: 0;
		font-size: 0.9rem;
	}

	li {
		display: flex;
		align-items: center;
		gap: 0.35rem;
		color: #888;
	}

	li:not(:last-child)::after {
		content: '/';
		color: #555;
	}

	a {
		color: #4fc3f7;
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}

	span {
		color: #e0e0e0;
		font-weight: 600;
	}
</style>
