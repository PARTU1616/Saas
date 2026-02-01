<template>
  <div class="q-pa-md">
    <div class="text-h5 q-mb-md">User Management</div>

    <q-table
      :rows="users"
      :columns="columns"
      row-key="id"
      flat
      bordered
      :loading="loading"
    >
      <template v-slot:body-cell-role="props">
        <q-td>
          <q-select
            dense
            outlined
            :model-value="props.row.role"
            :options="['ADMIN', 'USER']"
            @update:model-value="updateRole(props.row.id, $event)"
          />
        </q-td>
      </template>

      <template v-slot:body-cell-is_active="props">
        <q-td>
          <q-toggle
            v-model="props.row.is_active"
            @update:model-value="updateStatus(props.row.id, $event)"
          />
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const users = ref([])
const loading = ref(false)

const columns = [
  { name: 'email', label: 'Email', field: 'email', align: 'left' },
  { name: 'role', label: 'Role', field: 'role', align: 'center' },
  { name: 'is_active', label: 'Active', field: 'is_active', align: 'center' }
]

async function fetchUsers() {
  loading.value = true
  try {
    const res = await api.get('/users/')
    users.value = res.data.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Failed to fetch users'
    })
  } finally {
    loading.value = false
  }
}

async function updateRole(userId, role) {
  try {
    await api.put(`/users/${userId}/role`, { role })
    $q.notify({
      type: 'positive',
      message: 'Role updated successfully'
    })
    fetchUsers()
  } catch (error) {
    const message = error.response?.data?.error || 'Failed to update role'
    $q.notify({
      type: 'negative',
      message
    })
    fetchUsers() // Revert UI by re-fetching
  }
}

async function updateStatus(userId, isActive) {
  try {
    await api.put(`/users/${userId}/status`, { is_active: isActive })
    $q.notify({
      type: 'positive',
      message: 'Status updated successfully'
    })
  } catch (error) {
    const message = error.response?.data?.error || 'Failed to update status'
    $q.notify({
      type: 'negative',
      message
    })
    fetchUsers() // Revert UI by re-fetching
  }
}

onMounted(fetchUsers)
</script>
