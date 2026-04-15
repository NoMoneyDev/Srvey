export const RegisterUser = async (access_token: string) => {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token }),
    })

    const data = await res.json()
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user_picture", data.picture);
    localStorage.setItem("user_name", data.name);
    console.log("Response data:", data);
}