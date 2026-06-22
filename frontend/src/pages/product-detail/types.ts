interface IReportDepositForm {
  customerName: string
  customerPhone?: string | undefined
  depositAmount: number
  notes?: string | undefined
}

interface IReportCancellationForm {
  notes: string
}

export type { IReportDepositForm, IReportCancellationForm }
