
# --- 1. DATA ACQUISITION & PREPROCESSING ---
import wbgapi as wb
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches 
import matplotlib.lines as mlines

# Global Plotting Style
plt.style.use('fivethirtyeight')

#define a function to fetch and clean GDP data for given economy codes
def get_cleaned_gdp_data(economy_codes):
    """Fetches and cleans World Bank GDP growth data."""
    data = wb.data.DataFrame('NY.GDP.MKTP.KD.ZG', economy_codes, labels=True)
    data.index.name = 'economy'
    data = data.loc[:, data.columns.str.startswith('YR')]
    data.columns = data.columns.str.replace('YR', '').astype(int)
    return data

gdp_growth = get_cleaned_gdp_data(['MEA'])

# --- 2. CONFIGURATION & PARAMETERS ---
g_params = {
    'alpha': 0.7,
    'marker': 'o', 
    'markerfacecolor': 'white', 
    'markeredgecolor': '#2980b9', 
    'markersize': 7, 
    'markeredgewidth': 1,
    'color': '#377eb8',
    'linewidth': 1.5
}

# Shading for Global Crisis (Wide Area)
global_params = {
    'color': 'red', 
    'alpha': 0.15
}

# Styling for Middle East Crisis (Slim Line)
me_params = {
    'color': 'red',
    'alpha': 0.4,
    'linewidth': 1.5,
    'linestyle': '--'
}

t_params = {
    'color': 'black', 
    'fontsize': 9, 
    'va': 'center', 
    'ha': 'center'
}

# --- 3. PLOTTING FUNCTION ---
def plot_series(data, area, ylabel, ax, g_params, global_params, me_params, t_params, ylim=19, baseline=0):
    """Plots GDP with Global and Middle East crisis indicators."""
    
    # . Plot the main data line
    line_handle = None
    if area in data.index:
        line_handle, = ax.plot(data.loc[area], label=area, **g_params)
    
    # Define crises: (Start, End, Label, Type)
    # Types: 'global' for shaded area, 'me' for slim line
    crises = [
        (1973, 1975, 'Oil Crisis\n(1974)', 'global'),
        (1978, 1978, 'Iranian Revolution\n(1978)', 'me'),
        (1982, 1982, 'Lebanon War\n(1982)', 'me'),
        (1986, 1986, 'The Great Oil\nPrice Collapse\n(1986)', 'me'),
        (1990, 1992, '1990s recession\n(1991)', 'global'),
        (2007, 2009, 'GFC\n(2008)', 'global'),
        (2019, 2021, 'Covid-19\n(2020)', 'global')
    ]
    
    for i, (start, end, label, c_type) in enumerate(crises):
        if c_type == 'global':
            ax.axvspan(start, end, **global_params)
        else:
            # Draw slim line for Middle East specific crises
            ax.axvline(x=start, **me_params)
        
        # Staggered labels to avoid overlap
        stagger = 0.05 if i % 2 == 1 else 0.18
        label_year = (start + end) / 2
        ax.text(label_year, ylim + (ylim * stagger), label, **t_params)
        

    # . CREATE CUSTOM LEGEND
    # Proxy for Global Crisis (Box)
    global_patch = mpatches.Patch(color=global_params['color'], alpha=global_params['alpha'], label='Global Crisis')
    
    # Proxy for Middle East Crisis (Slim Line)
    me_line = mlines.Line2D([], [], color=me_params['color'], alpha=me_params['alpha'], 
                             linewidth=me_params['linewidth'], linestyle=me_params['linestyle'], 
                             label='Middle East Crisis')
    
    handles = [line_handle, global_patch, me_line]
    labels = [area, 'Global Crisis', 'Middle East Crisis']

    if ylim is not None:
        ax.set_ylim([-ylim, ylim + 5]) 

    if baseline is not None:
        ax.axhline(y=baseline, color='black', linestyle='--', linewidth=1)
    
    ax.set_ylabel(ylabel)
    ax.legend(handles=handles, labels=labels, loc='lower left', frameon=True, fontsize=10)
    
    return ax

# --- 4. EXECUTION ---
fig, ax = plt.subplots(figsize=(11, 8))

plot_series(
    data=gdp_growth, 
    area='MEA', 
    ylabel='GDP growth rate (%)', 
    ax=ax, 
    g_params=g_params, 
    global_params=global_params, 
    me_params=me_params,
    t_params=t_params
)

# Using bbox_inches='tight' in savefig is safer than tight_layout
plt.savefig('Business_Cycle_MEA_Full_Legend.png', dpi=300, bbox_inches='tight')
# Add source note at the bottom right of the figure
plt.figtext(0.95, 0.02, 'Source: World Bank', horizontalalignment='right', fontsize=9, style='italic', alpha=0.7)
plt.show()
