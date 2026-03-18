'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Navbar from '@/components/Navbar'

export default function DashboardPage() {
  const router = useRouter()
  const [userId, setUserId] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      router.push('/login')
      return
    }

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    fetch(`${apiUrl}/api/user/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Token invalid or expired')
        return res.json()
      })
      .then((data) => {
        setUserId(data.user_id || 'Unknown')
      })
      .catch((err) => {
        console.error('Auth check failed:', err)
        setError('Unauthorized. Please login again.')
        router.push('/login')
      })
  }, [router])

  return (
    <div>
      <Navbar />
      <div className="p-6">
        <h1 className="text-2xl font-bold">Welcome to your dashboard</h1>
        {error ? (
          <p className="text-red-600 mt-2">{error}</p>
        ) : (
          <>
            <p className="mt-2 text-gray-600">
              You can now manage job preferences, upload your resume, or let the AI apply for jobs.
            </p>
            <p className="mt-4 text-sm text-gray-500">User ID: {userId}</p>
          </>
        )}
      </div>
    </div>
  )
}
