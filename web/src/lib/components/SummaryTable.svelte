<script lang="ts">
	import type { SummaryData } from '$lib/types';

	let { location, data }: { location: string; data: SummaryData } = $props();

	const sensors: Record<string, string> = {
		temperature_f: 'Temperature',
		heat_index_f: 'Heat Index',
		humidity_pct: 'Humidity',
		pressure_inHg: 'Pressure'
	};

	const intervals = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR'];
</script>

<div class="table-wrap">
	<h2>{location} — high / low summary</h2>
	<table>
		<thead>
			<tr>
				<th>Sensor Reading</th>
				{#each intervals as interval}
					<th>{interval}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each Object.entries(sensors) as [key, label] (key)}
				<tr>
					<td>{label}</td>
					{#each intervals as interval}
						{@const cell = data[key]?.[interval]}
						<td>
							{#if cell}
								{@const parts = cell.split(' / ')}
								<span class="high">{parts[0]}</span>
								/
								<span class="low">{parts[1] ?? ''}</span>
							{:else}
								N/A
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.high {
		color: #ef5350;
	}

	.low {
		color: #4fc3f7;
	}
</style>
