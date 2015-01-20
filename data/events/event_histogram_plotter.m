

% Turn the high-resolution plot on or off
plot_high_res = false;

% Edit this value to change the amount each bar is offset [0,1]
quantize_offset = 0;

% Edit this value to change how many bars you will see on the histogram
quantize_bins =  24 * 1;




%-----------------------------------------
% No need to edit below this line
%-----------------------------------------
clf; hold on;

minutes_per_day = 60 * 24;
quantize_width = minutes_per_day ./ quantize_bins;

events_at_hour = zeros(1, quantize_bins);
quantize_offset_width = quantize_offset * quantize_width;

for i=1:minutes_per_day-1
    bin_index = floor((i + quantize_offset_width) ./ quantize_width) + 1;
    bin_index = mod(bin_index-1, quantize_bins)+1;
    events_at_hour(bin_index) = events_at_hour(bin_index) + events_at_minute(i);
end

bar_offset = (24 ./ (quantize_bins)) ./ 2;
x_histogram = linspace(bar_offset-quantize_offset, 24-bar_offset-quantize_offset, quantize_bins);
bar(x_histogram, events_at_hour, 1);


% -----------------------------------------
% This code block plots event data in high resolution (scaled to histogram
% plot above)
%-----------------------------------------
if plot_high_res
    x_minutely = linspace(0, 24, minutes_per_day);
    y_minutely = events_at_minute * quantize_width;
    bar_graph = bar(x_minutely, y_minutely, 1, 'EdgeColor', [1,0,0]);
    bar_child = get(bar_graph, 'child');
    set(bar_child, 'facea', 1); set(bar_child, 'edgea', 0.2);
end