// Signup Page
'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from '@/lib/api'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const router = useRouter()

  const handleSignup = async () => {
    try {
      const res = await axios.post('/auth/signup', { email, password })
      setMessage(res.data.message)
      setTimeout(() => router.push('/login'), 1500)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Signup failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded-xl shadow w-full max-w-md">
        <h1 className="text-xl font-bold mb-4 text-center">Sign Up</h1>
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
        {message && <p className="text-green-600 text-sm mb-2">{message}</p>}
        <button
          className="bg-green-600 text-white p-2 w-full rounded hover:bg-green-700"
          onClick={handleSignup}
        >
          Sign Up
        </button>
        <p className="text-center mt-3 text-sm">
          Already have an account? <a className="text-blue-600 underline" href="/login">Login</a>
        </p>
      </div>
    </div>
  )
}
