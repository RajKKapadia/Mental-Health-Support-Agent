"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { ArrowRight, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function ComingSoonPage() {
  const [email, setEmail] = useState("")
  const [submitted, setSubmitted] = useState(false)
  const [timeLeft, setTimeLeft] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  })

  // Set launch date to 30 days from now
  useEffect(() => {
    const launchDate = new Date()
    launchDate.setDate(launchDate.getDate() + 30)

    const timer = setInterval(() => {
      const now = new Date()
      const difference = launchDate.getTime() - now.getTime()

      if (difference <= 0) {
        clearInterval(timer)
        return
      }

      const days = Math.floor(difference / (1000 * 60 * 60 * 24))
      const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((difference % (1000 * 60)) / 1000)

      setTimeLeft({ days, hours, minutes, seconds })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically send the email to your backend
    console.log("Email submitted:", email)
    setSubmitted(true)
    setEmail("")

    // Reset the submitted state after 3 seconds
    setTimeout(() => {
      setSubmitted(false)
    }, 3000)
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-black text-white p-4">
      <div className="max-w-3xl mx-auto text-center space-y-12">
        <div className="space-y-6">
          <div className="inline-flex items-center px-3 py-1 rounded-full border border-zinc-800 bg-zinc-900/50 text-sm text-zinc-400 mb-4">
            <Sparkles className="h-3.5 w-3.5 mr-2" />
            <span>Something exciting is brewing</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-bold tracking-tighter">
            Something Interesting
            <span className="bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
              {" "}
              Is Coming Soon
            </span>
          </h1>

          <p className="text-zinc-400 text-lg md:text-xl max-w-2xl mx-auto">
            We're working on something amazing. Stay tuned for a revolutionary experience that will change the way you
            think about technology.
          </p>
        </div>

        <div className="grid grid-cols-4 gap-4 max-w-md mx-auto">
          <div className="flex flex-col items-center justify-center p-4 rounded-lg bg-zinc-900/50 border border-zinc-800">
            <span className="text-3xl font-bold">{timeLeft.days}</span>
            <span className="text-zinc-500 text-sm">Days</span>
          </div>
          <div className="flex flex-col items-center justify-center p-4 rounded-lg bg-zinc-900/50 border border-zinc-800">
            <span className="text-3xl font-bold">{timeLeft.hours}</span>
            <span className="text-zinc-500 text-sm">Hours</span>
          </div>
          <div className="flex flex-col items-center justify-center p-4 rounded-lg bg-zinc-900/50 border border-zinc-800">
            <span className="text-3xl font-bold">{timeLeft.minutes}</span>
            <span className="text-zinc-500 text-sm">Minutes</span>
          </div>
          <div className="flex flex-col items-center justify-center p-4 rounded-lg bg-zinc-900/50 border border-zinc-800">
            <span className="text-3xl font-bold">{timeLeft.seconds}</span>
            <span className="text-zinc-500 text-sm">Seconds</span>
          </div>
        </div>

        <div className="max-w-md mx-auto w-full">
          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2">
            <Input
              type="email"
              placeholder="Enter your email"
              className="bg-zinc-900/50 border-zinc-800 text-white"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Button
              type="submit"
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            >
              Notify Me <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </form>

          {submitted && <p className="text-green-400 mt-2 text-sm">Thanks! We'll notify you when we launch.</p>}

          <p className="text-zinc-500 text-xs mt-2">We'll never share your email with anyone else.</p>
        </div>
      </div>
    </div>
  )
}
