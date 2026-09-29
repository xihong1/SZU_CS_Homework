function isPrime(num) {
    if (num < 2) return false;
    if (num === 2) return true;
    if (num % 2 === 0) return false;
    for (var i = 3; i * i <= num; i += 2) {
        if (num % i === 0) return false;
    }
    return true;
}

self.onmessage = function (event) {
    var start = event.data.start;
    var end = event.data.end;
    var count = 0;

    for (var num = start; num <= end; num++) {
        if (isPrime(num)) {
            count++;
        }
        if (count > 0 && count % 1000 === 0) {
            self.postMessage({ type: "progress", current: num, end: end, count: count });
        }
    }

    self.postMessage({ type: "result", count: count });
};
