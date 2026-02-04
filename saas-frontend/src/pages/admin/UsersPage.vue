<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Users</div>

    <q-table
      flat
      bordered
      :rows="users"
      :columns="columns"
      row-key="id"
      :loading="loading"
    />
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const users = ref([])
const loading = ref(false)

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' },
  { name: 'email', label: 'Email', field: 'email' },
  { name: 'role', label: 'Role', field: 'role' },
  { name: 'is_active', label: 'Active', field: 'is_active' },
]

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/users/')
    users.value = res.data.data
  } finally {
    loading.value = false
  }
})
</script>
