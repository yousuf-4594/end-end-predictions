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

interface BillingRecord {
  customer_id: string
  contract_type: 'Month-to-month' | 'One year' | 'Two year'
  paperless_billing: boolean
  payment_method: 'Electronic check' | 'Mailed check' | 'Bank transfer (automatic)' | 'Credit card (automatic)'
}

export function BillingTable() {
  const [records, setRecords] = useState<BillingRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchBillingRecords = async () => {
      try {
        const response = await axios.get('http://localhost:8000/billing/')
        setRecords(response.data)
        setLoading(false)
      } catch (err) {
        setError('Failed to fetch billing records')
        setLoading(false)
      }
    }

    fetchBillingRecords()
  }, [])

  if (loading) return <div className="flex items-center justify-center p-4">Loading...</div>
  if (error) return <div className="flex items-center justify-center p-4 text-red-500">{error}</div>

  return (
    <ScrollArea className="h-[600px] w-full rounded-md border">
      <Table>
        <TableCaption>Billing Records List</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="whitespace-nowrap">Customer ID</TableHead>
            <TableHead className="whitespace-nowrap">Contract Type</TableHead>
            <TableHead className="whitespace-nowrap">Paperless Billing</TableHead>
            <TableHead className="whitespace-nowrap">Payment Method</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {records.map((record) => (
            <TableRow key={record.customer_id}>
              <TableCell>{record.customer_id}</TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-sm ${
                  record.contract_type === 'Two year'
                    ? 'bg-green-100 text-green-800'
                    : record.contract_type === 'One year'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {record.contract_type}
                </span>
              </TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-sm ${
                  record.paperless_billing
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {record.paperless_billing ? 'Yes' : 'No'}
                </span>
              </TableCell>
              <TableCell>{record.payment_method}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </ScrollArea>
  )
}