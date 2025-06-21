'use client'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function Navbar() {
  const router = useRouter()
  const [loggedIn, setLoggedIn] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    setLoggedIn(!!token)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    router.push('/login')
  }

  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <Link href="/dashboard" className="font-bold text-lg">AI Job Agent</Link>
      <div className="space-x-4">
        {loggedIn && (
          <>
            <Link href="/upload">Upload</Link>
            <Link href="/apply-log">Applied Jobs</Link>
            <Link href="/apply">Auto Apply</Link>
            <button onClick={handleLogout} className="bg-red-600 px-3 py-1 rounded">Logout</button>
          </>
        )}
        {!loggedIn && (
          <>
            <Link href="/login">Login</Link>
            <Link href="/signup">Signup</Link>
          </>
        )}
      </div>
    </nav>
  )
}