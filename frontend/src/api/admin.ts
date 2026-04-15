const API_URL = import.meta.env.VITE_API_URL

function getAuthHeaders() {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  }
}

export const adminAPI = {
  async getAllSurveys(page = 1, pageSize = 10) {
    const res = await fetch(
      `${API_URL}/admin/surveys?page=${page}&page_size=${pageSize}`,
      {
        headers: getAuthHeaders()
      }
    )

    if (!res.ok) throw new Error(`Error ${res.status}`)

    return await res.json()
  },

  async getAllUsers(page = 1, pageSize = 10) {
    const res = await fetch(
      `${API_URL}/admin/users?page=${page}&page_size=${pageSize}`,
      {
        headers: getAuthHeaders()
      }
    )

    if (!res.ok) throw new Error(`Error ${res.status}`)

    return await res.json()
  },

  async deleteUser(userId: string) {
    const res = await fetch(
      `${API_URL}/admin/users/${userId}`,
      {
        method: 'DELETE',
        headers: getAuthHeaders()
      }
    )

    if (!res.ok) throw new Error(`Error ${res.status}`)

    return await res.json()
  },

  async deleteSurvey(surveyId: string) {
    const res = await fetch(
      `${API_URL}/admin/surveys/${surveyId}`,
      {
        method: 'DELETE',
        headers: getAuthHeaders()
      }
    )

    if (!res.ok) throw new Error(`Error ${res.status}`)

    return await res.json()
  },

  async getSurveyQuestions(surveyId: string) {
    const res = await fetch(
      `${API_URL}/admin/surveys/${surveyId}/questions`,
      {
        headers: await getAuthHeaders()
      }
    )

    if (!res.ok) throw new Error(`Error ${res.status}`)

    return await res.json()
  }
}