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

interface PhoneService {
  customer_id: string
  has_phone_service: boolean
  multiple_lines: 'No phone service' | 'No' | 'Yes'
}

export function PhoneServicesTable() {
  const [services, setServices] = useState<PhoneService[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPhoneServices = async () => {
      try {
        const response = await axios.get('http://localhost:8000/phone-services/')
        setServices(response.data)
        setLoading(false)
      } catch (err) {
        setError('Failed to fetch phone services')
        setLoading(false)
      }
    }

    fetchPhoneServices()
  }, [])

  if (loading) return <div className="flex items-center justify-center p-4">Loading...</div>
  if (error) return <div className="flex items-center justify-center p-4 text-red-500">{error}</div>

  return (
    <ScrollArea className="h-[600px] w-full rounded-md border">
      <Table>
        <TableCaption>Phone Services List</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="whitespace-nowrap">Customer ID</TableHead>
            <TableHead className="whitespace-nowrap">Phone Service</TableHead>
            <TableHead className="whitespace-nowrap">Multiple Lines</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {services.map((service) => (
            <TableRow key={service.customer_id}>
              <TableCell>{service.customer_id}</TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-sm ${
                  service.has_phone_service
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {service.has_phone_service ? 'Yes' : 'No'}
                </span>
              </TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-sm ${
                  service.multiple_lines === 'Yes'
                    ? 'bg-green-100 text-green-800'
                    : service.multiple_lines === 'No'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {service.multiple_lines}
                </span>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </ScrollArea>
  )
}