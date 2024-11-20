"use client"

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { ScrollArea } from "@/components/ui/scroll-area"

interface InternetService {
  customer_id: string
  internet_service: 'DSL' | 'Fiber optic' | 'No'
  online_security: 'No' | 'Yes' | 'No internet service'
  online_backup: 'No' | 'Yes' | 'No internet service'
  device_protection: 'No' | 'Yes' | 'No internet service'
  tech_support: 'No' | 'Yes' | 'No internet service'
  streaming_tv: 'No' | 'Yes' | 'No internet service'
  streaming_movies: 'No' | 'Yes' | 'No internet service'
}

export function InternetServicesTable() {
  const [services, setServices] = useState<InternetService[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchInternetServices = async () => {
      try {
        const response = await axios.get('http://localhost:8000/internet-services/')
        setServices(response.data)
        setLoading(false)
      } catch (err) {
        setError('Failed to fetch internet services')
        setLoading(false)
      }
    }

    fetchInternetServices()
  }, [])

  if (loading) return <div className="flex items-center justify-center p-4">Loading...</div>
  if (error) return <div className="flex items-center justify-center p-4 text-red-500">{error}</div>

  return (
    <ScrollArea className="h-[600px] w-full rounded-md border">
      <Table>
        <TableCaption>Internet Services List</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="whitespace-nowrap">Customer ID</TableHead>
            <TableHead className="whitespace-nowrap">Internet Service</TableHead>
            <TableHead className="whitespace-nowrap">Online Security</TableHead>
            <TableHead className="whitespace-nowrap">Online Backup</TableHead>
            <TableHead className="whitespace-nowrap">Device Protection</TableHead>
            <TableHead className="whitespace-nowrap">Tech Support</TableHead>
            <TableHead className="whitespace-nowrap">Streaming TV</TableHead>
            <TableHead className="whitespace-nowrap">Streaming Movies</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {services.map((service) => (
            <TableRow key={service.customer_id}>
              <TableCell>{service.customer_id}</TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-sm ${
                  service.internet_service === 'Fiber optic' 
                    ? 'bg-green-100 text-green-800'
                    : service.internet_service === 'DSL'
                    ? 'bg-blue-100 text-blue-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {service.internet_service}
                </span>
              </TableCell>
              <TableCell>{service.online_security}</TableCell>
              <TableCell>{service.online_backup}</TableCell>
              <TableCell>{service.device_protection}</TableCell>
              <TableCell>{service.tech_support}</TableCell>
              <TableCell>{service.streaming_tv}</TableCell>
              <TableCell>{service.streaming_movies}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </ScrollArea>
  )
}