import sortedcontainers as sc


def get_col_binner(bin_list):
    sorted_bins = sc.SortedList(bin_list)
    last_ix = len(sorted_bins) - 1

    def _col_binner(val):
        if val in sorted_bins:
            ind = sorted_bins.bisect(val) - 1
            if ind == last_ix:
                return f"{sorted_bins[-1]}≤"
            return f"{sorted_bins[ind]}-{sorted_bins[ind + 1]}"
        try:
            ind = sorted_bins.bisect(val)
            if ind == 0:
                return f"<{sorted_bins[ind]}"
            return f"{sorted_bins[ind - 1]}-{sorted_bins[ind]}"
        except IndexError:
            return f"{sorted_bins[sorted_bins.bisect(val) - 1]}≤"

    return _col_binner
