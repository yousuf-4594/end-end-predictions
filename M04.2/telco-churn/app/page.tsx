'use client'
import Image from "next/image";
import { useState, useEffect } from "react";
import { RefreshCcw } from "lucide-react"; // Import the refresh icon
import { AppSidebar } from "@/components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar" 
import Chatcomponent from "@/components/chat";

export default function Home() {
  const [isApiActive, setIsApiActive] = useState(false);

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/status");
        if (response.ok) {
          setIsApiActive(true);
        } else {
          setIsApiActive(false);
        }
      } catch {
        setIsApiActive(false);
      }
    };

    checkApiStatus();
    const intervalId = setInterval(checkApiStatus, 30000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex sticky top-0 bg-background h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem className="hidden md:block">
                <BreadcrumbLink href="#">
                  Dashboard
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator className="hidden md:block" />
 
            </BreadcrumbList>
          </Breadcrumb>
          <div className="flex items-center gap-4 ml-auto border-dotted rounded-lg p-2 bg-gray-100">
            <div className="flex items-center gap-2">
              <span>Status</span>
              <span
                className={`w-3 h-3 rounded-full ${isApiActive ? "bg-green-500" : "bg-red-500"}`}
              />
            </div>
          </div>

        </header>
        <div>
        <Chatcomponent/>
        </div>
        
      </SidebarInset>
    </SidebarProvider>
  );
}
