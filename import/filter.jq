.Transaction
.TradeMarkTransactionBody
.TransactionContentDetails
.TransactionData
.TradeMarkDetails
.TradeMark
| select(.MarkFeature == "Word")
| [
    .ApplicationNumber,
    .WordMarkSpecification.MarkVerbalElementText,
    .ApplicationDate,
    .RegistrationDate,
    .ExpiryDate
]
| @csv
