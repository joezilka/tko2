import os
import streamlit as st
import pandas as pd
from snowflake.snowpark.session import Session


#use your variable name

cp = {
    "account": os.getenv("SFACCOUNT"),
    "user": os.getenv("SFUSER"),
    "password": os.getenv("SFPWD"),
    "role": os.getenv("SFROLE"),
    "warehouse": os.getenv("SFWAREHOUSE")
}


def exec_sql(sess, query):
    try:
        rowset=sess.sql(query)
    except Exception as e:
            st.error("Oops! ", query, "error executing", str(e), "occurred.")
            return pd.DataFrame()
    else:
        try:
            tdf = pd.DataFrame(rowset.collect())
        except Exception as e1:
                st.error(str(e1))
                return pd.DataFrame()
        else:
            return tdf
    return


def create_session():
    session = Session.builder.configs(cp).create()
    session.query_tag="streamlit testing"
    return session

sess = create_session()


query = "select * from snowflake.account_usage.users;"

df = exec_sql(sess,query)

# Print results.
st.dataframe(df)

st.snow()