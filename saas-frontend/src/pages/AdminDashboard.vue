<template>
  <div class="q-pa-md">
    <h4>Admin Dashboard</h4>

    <q-card class="q-mt-md">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Organization Users</div>
        <q-space />
        <q-btn
          color="primary"
          label="Add User"
          icon="add"
          @click="showAddDialog = true"
        />
      </q-card-section>

      <q-separator />

      <q-card-section>
        <q-table
          :rows="users"
          :columns="columns"
          row-key="id"
          :loading="loading"
        >
          <template #body-cell-actions="props">
            <q-td :props="props" class="q-gutter-x-sm">
              <q-btn
                v-if="props.row.id !== auth.user?.id"
                size="sm"
                flat
                color="primary"
                label="Toggle Role"
                @click="toggleRole(props.row)"
              />

              <q-btn
                v-if="props.row.id !== auth.user?.id"
                size="sm"
                flat
                :color="props.row.is_active ? 'negative' : 'positive'"
                :label="props.row.is_active ? 'Deactivate' : 'Activate'"
                @click="toggleStatus(props.row)"
              />
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <q-dialog v-model="showAddDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Add New User</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            dense
            v-model="newUser.email"
            label="Email"
            type="email"
            autofocus
            :rules="[val => !!val || 'Email is required']"
          />
          <q-input
            dense
            v-model="newUser.password"
            label="Password"
            type="password"
            class="q-mt-sm"
            :rules="[val => !!val || 'Password is required']"
          />
          <q-select
            dense
            v-model="newUser.role"
            :options="['USER', 'ADMIN']"
            label="Role"
            class="q-mt-sm"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup @click="resetForm" />
          <q-btn flat label="Add User" @click="addUser" :loading="submitting" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth'

const $q = useQuasar()
const auth = useAuthStore()
const users = ref([])
const loading = ref(false)
const submitting = ref(false)
const showAddDialog = ref(false)

const newUser = ref({
  email: '',
  password: '',
  role: 'USER'
})

const columns = [
  { name: 'email', label: 'Email', field: 'email', align: 'left' },
  { name: 'role', label: 'Role', field: 'role', align: 'left' },
  { name: 'is_active', label: 'Active', field: 'is_active', align: 'left' },
  { name: 'actions', label: 'Actions', field: 'id', align: 'center' }
]

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await api.get('/users/')
    users.value = res.data.data
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to fetch users',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)

const resetForm = () => {
  newUser.value = {
    email: '',
    password: '',
    role: 'USER'
  }
}

const addUser = async () => {
  if (!newUser.value.email || !newUser.value.password) {
    $q.notify({
      color: 'warning',
      message: 'Please fill in all fields'
    })
    return
  }

  submitting.value = true
  try {
    await api.post('/users/', newUser.value)
    $q.notify({
      color: 'positive',
      message: 'User added successfully',
      icon: 'check'
    })
    showAddDialog.value = false
    resetForm()
    await fetchUsers()
  } catch (err) {
    $q.notify({
      color: 'negative',
      message: err.response?.data?.error || 'Failed to add user',
      icon: 'error'
    })
  } finally {
    submitting.value = false
  }
}

const toggleRole = async (user) => {
  const newRole = user.role === 'ADMIN' ? 'USER' : 'ADMIN'
  loading.value = true
  try {
    await api.put(`/users/${user.id}/role`, { role: newRole })
    $q.notify({
      color: 'positive',
      message: `Role updated to ${newRole}`,
      icon: 'check'
    })
    await fetchUsers()
  } catch (err) {
    $q.notify({
      color: 'negative',
      message: err.response?.data?.error || 'Failed to update role',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}

const toggleStatus = async (user) => {
  const newStatus = !user.is_active
  loading.value = true
  try {
    await api.put(`/users/${user.id}/status`, { is_active: newStatus })
    $q.notify({
      color: 'positive',
      message: `User ${newStatus ? 'activated' : 'deactivated'}`,
      icon: 'check'
    })
    await fetchUsers()
  } catch (err) {
    $q.notify({
      color: 'negative',
      message: err.response?.data?.error || 'Failed to update status',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>
