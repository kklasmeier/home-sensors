<script lang="ts">
	let {
		open = $bindable(false),
		content = ''
	}: {
		open?: boolean;
		content?: string;
	} = $props();

	let logEl = $state<HTMLPreElement | null>(null);

	$effect(() => {
		if (open && logEl) {
			logEl.scrollTop = logEl.scrollHeight;
		}
	});

	function onBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			open = false;
		}
	}
</script>

{#if open}
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<div class="backdrop" role="presentation" onclick={onBackdropClick}>
		<div class="modal" role="dialog" aria-modal="true" aria-labelledby="log-title">
			<div class="modal-header">
				<h2 id="log-title">Collector Log</h2>
				<button type="button" onclick={() => (open = false)}>Close</button>
			</div>
			<pre bind:this={logEl}><code>{content}</code></pre>
		</div>
	</div>
{/if}

<style>
	.backdrop {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.75);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		padding: 1rem;
	}

	.modal {
		background: #1e1e1e;
		border: 1px solid #444;
		border-radius: 8px;
		width: min(95vw, 900px);
		max-height: 85vh;
		display: flex;
		flex-direction: column;
	}

	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		border-bottom: 1px solid #333;
	}

	.modal-header h2 {
		margin: 0;
		font-size: 1.1rem;
	}

	pre {
		margin: 0;
		padding: 1rem;
		overflow: auto;
		flex: 1;
		font-size: 0.8rem;
		line-height: 1.4;
		background: #121212;
	}

	code {
		color: #c5e1a5;
		white-space: pre-wrap;
		word-break: break-word;
	}
</style>
