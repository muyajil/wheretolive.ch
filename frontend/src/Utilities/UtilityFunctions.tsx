function range(start: number, stop: number, step: number) {
    if (typeof stop == 'undefined') {
        // one param defined
        stop = start;
        start = 0;
    }

    if (typeof step == 'undefined') {
        step = 1;
    }

    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
        return [];
    }

    const numEdges = (stop/step)
    var result = new Array(numEdges)
    for (var i = 0; i < numEdges; i++) {
        result[i] = i*step
    }

    return result;
};

function renderMinutes(inputMins: number) {
    var hours = Math.floor(inputMins / 60);
    var minutes = inputMins % 60;
    return (
        ("0" + hours).slice(-2)+":"+("0" + minutes).slice(-2) + " h"
    );
  }

export {range, renderMinutes};