import pandas as pd
df = pd.DataFrame({'rainy': [.4, .7], 
                   'sunny': [.6, .3]
                  }, 
                  index=["rainy", "sunny"])
print df

print df.dot(df)

df_market = pd.DataFrame({'bull': [.9,.15,.25], 'bear': [.075,.8,.25], 'stagnant': [.025,.05,.5]}, index=["bull", "bear", "stagnant"])

print df_market

print df_market.dot(df_market.dot(df_market.dot(df_market.dot(df_market))))
# probabilities after 2 transitions:
#bull      0.13375  0.8275   0.03875
#bear      0.66375  0.2675   0.06875
#stagnant  0.34375  0.3875   0.26875

# probabilities after 5 transitions