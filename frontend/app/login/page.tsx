'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from '@/lib/api'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  const handleLogin = async () => {
    try {
      const res = await axios.post('/auth/login', { email, password })
      localStorage.setItem('access_token', res.data.access_token)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded-xl shadow w-full max-w-md">
        <h1 className="text-xl font-bold mb-4 text-center">Login</h1>
        <input
          type="email"
          placeholder="Email"
          className="w-full border p-2 mb-3 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full border p-2 mb-3 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <button
          className="bg-blue-600 text-white p-2 w-full rounded hover:bg-blue-700"
          onClick={handleLogin}
        >
          Login
        </button>
        <p className="text-center mt-3 text-sm">
          No account? <a className="text-blue-600 underline" href="/signup">Sign up</a>
        </p>
      </div>
    </div>
  )
}
