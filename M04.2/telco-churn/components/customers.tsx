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
import { Button } from "@/components/ui/button"

interface Customer {
  customer_id: string
  gender: string
  is_senior_citizen: boolean
  has_partner: boolean
  has_dependents: boolean
  tenure: number
  monthly_charges: number
  total_charges: number
}

export function CustomersTable() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await axios.get('http://localhost:8000/customers/')
        console.log(response.data);
        setCustomers(response.data)
        setLoading(false)
      } catch (err) {
        setError('Failed to fetch customers')
        setLoading(false)
      }
    }

    fetchCustomers()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>{error}</div>

  return (
    <ScrollArea className="h-[600px] w-full rounded-md border">
      <Table>
        <TableCaption>List of Customers</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Customer ID</TableHead>
            <TableHead>Gender</TableHead>
            <TableHead>Senior Citizen</TableHead>
            <TableHead>Partner</TableHead>
            <TableHead>Dependents</TableHead>
            <TableHead>Tenure</TableHead>
            <TableHead>Monthly Charges</TableHead>
            <TableHead>Total Charges</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {customers.map((customer) => (
            <TableRow key={customer.customer_id}>
              <TableCell>{customer.customer_id}</TableCell>
              <TableCell>{customer.gender}</TableCell>
              <TableCell>{customer.is_senior_citizen ? 'Yes' : 'No'}</TableCell>
              <TableCell>{customer.has_partner ? 'Yes' : 'No'}</TableCell>
              <TableCell>{customer.has_dependents ? 'Yes' : 'No'}</TableCell>
              <TableCell>{customer.tenure}</TableCell>
              <TableCell>${customer.monthly_charges.toFixed(2)}</TableCell>
              <TableCell>${customer.total_charges.toFixed(2)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </ScrollArea>
  )
}