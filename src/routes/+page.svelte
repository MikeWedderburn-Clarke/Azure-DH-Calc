<script lang="ts">
  let region = 'westeurope';
  let currency = 'GBP';
  let vmSku = '';
  let count = 1;

  function calculate() {
    alert(`Region: ${region}, Currency: ${currency}, VM: ${vmSku}, Count: ${count}`);
  }
</script>

<div class="p-6 max-w-lg mx-auto">
  <h1 class="text-2xl font-bold mb-4">Azure DH Calculator</h1>
  <form on:submit|preventDefault={calculate} class="space-y-4">
    <input class="input" placeholder="Region" bind:value={region} />
    <input class="input" placeholder="Currency" bind:value={currency} />
    <input class="input" placeholder="VM SKU" bind:value={vmSku} />
    <input class="input" type="number" min="1" bind:value={count} />
    <button class="btn">Calculate</button>
  </form>
</div>

<style>
.input { @apply border p-2 w-full; }
.btn { @apply bg-blue-600 text-white px-4 py-2 rounded; }
</style>
