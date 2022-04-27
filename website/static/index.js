function deleteStock(stockId) {
    fetch("/delete-stock", {
        method: "POST",
        body: JSON.stringify({ stockId: stockId}),
    }).then((_res) => {
        window.location.href = "/";
    });

}

function getPrice(ticker) {
    fetch('/get-price', {
        method: 'GET',
        body: JSON.stringify({ticker: ticker}),
    });
}