"use client"

import { columns } from "../../components/columns";
import { ChartArea } from "../../components/chart-area";
import { ChartBar } from "../../components/chart-bar";

import { useEffect, useState } from "react";
import { ChartLine } from "../../components/chart-line";
import { DataTable } from "../../components/data-table";
import { Upload } from "lucide-react"
import { Button } from "@/components/ui/button"
import UploadDialog from "../../components/uploadDialog";

function getData() {
  // Fetch data from your API here.
  return [
    {
      transaction_date: "2025-01-01",
      amount: 100,
      status: "pending",
      category: "Food",
      payee: "Himalayan Java",
      type_of_transaction: "Debit",
      payment_method: "QR"
    },
    {
      transaction_date: "2025-01-02",
      amount: 100,
      status: "pending",
      category: "Grocery",
      payee: "BBSM",
      type_of_transaction: "Debit",
      payment_method: "QR"
    },
  ];
}


export default function Home() {
  const [categoryBarChartData, setCategoryBarChartData] = useState([]);
  const [paymentMethodBarChartData, setPaymentMethodBarChartData] = useState([]);
  const [expensesLineChartData, setExpensesLineChartData] = useState([]);
  const [transactionTableList, setTransactionTableList] = useState([]);
  const [isUploadOpen, setIsUploadOpen] = useState(false); 

  const chartData = [
    { date: "January", amount: 186 },
    { date: "February", amount: 305 },
    { date: "March", amount: 237 },
    { date: "April", amount: 73 },
    { date: "May", amount: 209 },
    { date: "June", amount: 214 },
  ]

  const updateUploadState = (uploadState) => {
    setIsUploadOpen(uploadState)
  }

  useEffect(() => {
    fetch("http://localhost:8001/expenses/category/")
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        console.log("Fetched data: ", data);
        setCategoryBarChartData(data);
      })
      .catch(error => console.log("Error fetching expenses:", error));
  }, [])

  useEffect(() => {
    fetch("http://localhost:8001/expenses/payment-method/")
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        console.log("Fetched Payment method data: ", data);
        setPaymentMethodBarChartData(data);
      })
      .catch(error => console.log("Error fetching expenses:", error));
  }, [])

  useEffect(() => {
    fetch("http://localhost:8001/expenses/")
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        console.log("Fetched Payment method data: ", data);
        setExpensesLineChartData(data);
      })
      .catch(error => console.log("Error fetching expenses:", error));
  }, [])

  useEffect(() => {
    fetch("http://localhost:8001/transactions/")
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        console.log("Fetched data: ", data);
        setTransactionTableList(data);
      })
      .catch(error => console.log("Error fetching expenses:", error));
  }, [])

  const tableData = getData();

  return (
    <>
    <main className="min-h-screen p-8">
      <UploadDialog updateUploadState={updateUploadState} isUploadOpen={isUploadOpen}/>
      <div className="flex justify-end md:fixed md:right-8 md:top-8">
        <Button onClick={() => setIsUploadOpen(true)} className="flex items-center gap-2">
          <Upload className="w-4 h-4" />
          Upload Statement
        </Button>
      </div>
    <div className="flex min-h-svh items-center justify-center p-6 flex-col w-full">
  {/* Charts Grid */}
  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-4xl">
    <ChartBar chartData={categoryBarChartData} title="Bar Chart - Category" dataKey="category" />
    <ChartBar chartData={paymentMethodBarChartData} title="Bar Chart - Payment Method" dataKey="payment_method" />
    <ChartLine chartData={expensesLineChartData} XAxisDataKey="date" LineDataKey="amount" />
  </div>

  {/* DataTable in a separate row */}
    <div className="w-full max-w-4xl mt-6">
      <DataTable columns={columns} data={transactionTableList} />
    </div>
</div>
  </main>
    </>
  );
}
