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
    >
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn
            dense
            size="sm"
            color="primary"
            label="Make Admin"
            v-if="props.row.role === 'USER'"
            @click="changeRole(props.row.id, 'ADMIN')"
          />

          <q-btn
            dense
            size="sm"
            color="negative"
            label="Make User"
            v-if="props.row.role === 'ADMIN'"
            @click="changeRole(props.row.id, 'USER')"
          />
        </q-td>
      </template>
    </q-table>
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
  { name: 'actions', label: 'Actions', field: 'actions' },
]

async function changeRole(userId, role) {
  try {
    await api.patch(`/admin/users/${userId}/role`, { role })

    // 🔄 Refresh users
    const res = await api.get('/users/')
    users.value = res.data.data
  } catch (err) {
    alert(err.response?.data?.error || 'Action failed')
  }
}

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
