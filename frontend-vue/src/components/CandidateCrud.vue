<template>
    <div>
      <h2>Candidate CRUD</h2>
      <div>
        <button @click="openCreateModal">Add New Candidate</button>
      </div>
  
      <!-- Table to display candidates -->
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Vice Name</th>
            <th>Vision</th>
            <th>Mission</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="candidate in candidates" :key="candidate.id">
            <td>{{ candidate.name }}</td>
            <td>{{ candidate.vice_name }}</td>
            <td>{{ candidate.vision }}</td>
            <td>{{ candidate.mission }}</td>
            <td>
              <button @click="openEditModal(candidate)">Edit</button>
              <button @click="deleteCandidate(candidate.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Modal for Create/Edit Candidate -->
      <div v-if="showModal">
        <h3>{{ isEdit ? 'Edit' : 'Add' }} Candidate</h3>
        <input v-model="form.name" placeholder="Name" />
        <input v-model="form.vice_name" placeholder="Vice Name" />
        <textarea v-model="form.vision" placeholder="Vision"></textarea>
        <textarea v-model="form.mission" placeholder="Mission"></textarea>
        <button @click="saveCandidate">Save</button>
        <button @click="closeModal">Cancel</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        candidates: [],
        form: {
          name: '',
          vice_name: '',
          vision: '',
          mission: ''
        },
        isEdit: false,
        showModal: false,
        currentCandidateId: null
      };
    },
    mounted() {
      this.fetchCandidates();
    },
    methods: {
      // Fetch candidates from the API
      async fetchCandidates() {
        try {
          const response = await axios.get('http://localhost:8000/api/candidates/');
          this.candidates = response.data;
        } catch (error) {
          console.error('Error fetching candidates:', error);
        }
      },
  
      // Open modal for creating a new candidate
      openCreateModal() {
        this.form = { name: '', vice_name: '', vision: '', mission: '' };
        this.isEdit = false;
        this.showModal = true;
      },
  
      // Open modal for editing an existing candidate
      openEditModal(candidate) {
        this.form = { ...candidate };
        this.isEdit = true;
        this.showModal = true;
        this.currentCandidateId = candidate.id;
      },
  
      // Save new or edited candidate
      async saveCandidate() {
        if (this.isEdit) {
          // Update candidate
          try {
            await axios.put(`http://localhost:8000/api/candidates/${this.currentCandidateId}/`, this.form);
            this.fetchCandidates();
            this.closeModal();
          } catch (error) {
            console.error('Error updating candidate:', error);
          }
        } else {
          // Create new candidate
          try {
            await axios.post('http://localhost:8000/api/candidates/', this.form);
            this.fetchCandidates();
            this.closeModal();
          } catch (error) {
            console.error('Error creating candidate:', error);
          }
        }
      },
  
      // Delete candidate
      async deleteCandidate(id) {
        try {
          await axios.delete(`http://localhost:8000/api/candidates/${id}/`);
          this.fetchCandidates();
        } catch (error) {
          console.error('Error deleting candidate:', error);
        }
      },
  
      // Close modal
      closeModal() {
        this.showModal = false;
        this.form = { name: '', vice_name: '', vision: '', mission: '' };
        this.currentCandidateId = null;
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  </style>
  