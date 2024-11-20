import { useState, useEffect } from 'react';
import { TrendingUp } from "lucide-react";
import { Bar, BarChart, XAxis, YAxis } from "recharts";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

interface DemographicData {
  category: 'has_partner' | 'has_dependents' | 'is_senior';
  count: number;
  fill: string;
}

type ChartConfigType = {
  count: {
    label: string;
  };
  has_partner: {
    label: string;
    color: string;
  };
  has_dependents: {
    label: string;
    color: string;
  };
  is_senior: {
    label: string;
    color: string;
  };
}

const chartConfig: ChartConfigType = {
  count: {
    label: "Count",
  },
  has_partner: {
    label: "Has Partner",
    color: "hsl(var(--chart-1))",
  },
  has_dependents: {
    label: "Has Dependents",
    color: "hsl(var(--chart-2))",
  },
  is_senior: {
    label: "Senior Citizen",
    color: "hsl(var(--chart-3))",
  }
} as const;

export default function CustomerDemographics() {
  const [chartData, setChartData] = useState<DemographicData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/customer-demographics')
      .then(response => response.json())
      .then((data: DemographicData[]) => {
        setChartData(data);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return <div className="p-4">Loading...</div>;
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Customer Demographics</CardTitle>
        <CardDescription>Customer Segment Distribution</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart
            accessibilityLayer
            data={chartData}
            layout="vertical"
            margin={{
              left: 20,
              right: 20,
              top: 5,
              bottom: 5,
            }}
            height={200}
          >
            <YAxis
              dataKey="category"
              type="category"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={(value: keyof typeof chartConfig) => 
                chartConfig[value]?.label || value
              }
            />
            <XAxis dataKey="count" type="number" />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Bar dataKey="count" layout="vertical" radius={5} />
          </BarChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col items-start gap-2 text-sm">
        <div className="flex gap-2 font-medium leading-none">
          Customer Segment Analysis <TrendingUp className="h-4 w-4" />
        </div>
        <div className="leading-none text-muted-foreground">
          Showing distribution of customer demographic segments
        </div>
      </CardFooter>
    </Card>
  );
}