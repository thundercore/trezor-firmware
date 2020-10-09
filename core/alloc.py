#!/usr/bin/env python3

from types import SimpleNamespace
import click


def parse_alloc_data(alloc_data):
    parsed_data = {}
    for line in alloc_data:
        ident, allocs, calls = line.strip().split(" ")
        allocs = int(allocs)
        calls = int(calls)
        filename, lineno = ident.split(":")
        lineno = int(lineno)

        filedata = parsed_data.setdefault(filename, {})
        filedata[lineno] = {
            "total_allocs": allocs,
            "total_calls": calls,
            "avg_allocs": allocs / calls,
        }
    return parsed_data


@click.group()
@click.pass_context
@click.option("-a", "--alloc-data", type=click.File(), default="src/alloc_data.txt")
@click.option("-t", "--type", type=click.Choice(("total", "avg")), default="avg")
def cli(ctx, alloc_data, type):
    ctx.obj = SimpleNamespace(data=parse_alloc_data(alloc_data), type=type)


@cli.command()
@click.pass_obj
@click.argument("filename")
@click.option("-c", "--calls", is_flag=True, help="include times called as first value")
def annotate(obj, filename, calls):
    if obj.type == "total":
        alloc_str = lambda line: str(line["total_allocs"])
    else:
        alloc_str = lambda line: "{:.2f}".format(line["avg_allocs"])

    if filename.startswith("src/"):
        filename = filename[4:]
    filedata = obj.data[filename]

    linedata = {lineno: alloc_str(line) for lineno, line in filedata.items()}
    maxlen = max(len(l) for l in linedata.values())

    call_nos = {lineno: str(line["total_calls"]) for lineno, line in filedata.items()}
    max_call = max(len(l) for l in call_nos.values())

    lineno = 0
    for line in open("src/" + filename):
        lineno += 1
        linecount = linedata.get(lineno, "")
        callcount = call_nos.get(lineno, "")
        if calls:
            callcount_str = f"{callcount:{max_call}} "
        else:
            callcount_str = ""
        print(f"{callcount_str}{linecount:{maxlen}}  {line}", end="")


@cli.command()
@click.pass_obj
@click.option("-r", "--reverse", is_flag=True)
def list(obj, reverse):
    if obj.type == "total":
        field = "total_allocs"
        field_fmt = "{}"
    else:
        field = "avg_allocs"
        field_fmt = "{:.2f}"

    file_sums = {
        filename: sum(line[field] for line in lines.values())
        for filename, lines in obj.data.items()
    }

    maxlen = max(len(field_fmt.format(l)) for l in file_sums.values())

    for filename, file_sum in sorted(
        file_sums.items(), key=lambda x: x[1], reverse=reverse
    ):
        num_str = field_fmt.format(file_sum)
        print(f"{num_str:>{maxlen}}  {filename}")


if __name__ == "__main__":
    cli()
