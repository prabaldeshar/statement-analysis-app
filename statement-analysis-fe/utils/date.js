function convertDateTimeStringToDate(datetimeString) {
    const date = new Date(datetimeString);
    const dateOnly = date.toLocaleDateString();
    return dateOnly
}

function convertDateTimeStringToMonthDay(datetimeString) {
    const date = new Date(datetimeString);
    const month = date.getMonth() + 1; // getMonth() returns 0-based month
    const day = date.getDate();
    return `${month}/${day}`;
}

export {convertDateTimeStringToMonthDay};