<script lang="ts">
	import type { GarageDoor } from '$lib/types';

	let { doors }: { doors: GarageDoor[] } = $props();
</script>

<div class="garage-panel">
	{#each doors as door (door.column)}
		<div class="garage-door">
			<h3>{door.label}</h3>
			<img src="/{door.image}" alt={door.status} />
			<p class="status">{door.status}</p>
			<p class="duration">{door.duration}</p>
		</div>
	{/each}
</div>

<style>
	.garage-panel {
		display: flex;
		flex-wrap: wrap;
		gap: 2rem;
		justify-content: center;
		margin-bottom: 2rem;
	}

	.garage-door {
		text-align: center;
	}

	.garage-door img {
		max-width: 200px;
		height: auto;
		border-radius: 8px;
	}

	.status {
		font-weight: 600;
		margin: 0.5rem 0 0.25rem;
	}

	.duration {
		color: #aaa;
		margin: 0;
	}
</style>
