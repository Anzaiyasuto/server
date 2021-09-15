from flask import Flask, request, render_template
import math
app = Flask(__name__)
file_path = "./sensor_data.csv"
port_num = 18011
state = ""

@app.route('/', methods=['GET'])
def get_html():
    return render_template('./index.html')

@app.route('/lux', methods=['POST'])
def update_lux():
    flag = ['vacant', 'occupied'] #flag = 0 -> vacant | flag = 1 -> occupied 
    time = request.form["time"]
    lux = request.form["lux"]
    #print(type(lux))
    
    lux = float(lux)

    alpha = None
    beta = None
    theta = None #str lux
    delta = None #occupied or vacant
    ganma = None #float lux
    temp = None
    try:
        f = open(file_path, 'r')
        for row in f:
            alpha = row
        beta = alpha.split(',')
        theta = beta[1]
        delta = beta[2]
        ganma = float(theta)
    except Exception as e:
        print(e)
    finally:
        f.close()
    
    print("debug")
    if(math.fabs(lux-beta) < 50):
        temp = delta
    else:
        if(theta == flag[0]):
            temp = flag[1]
        else:
            temp = flag[0]    

    try:
        f = open(file_path, 'w')
        f.write(time + "," + str(lux) + "," + temp)
        return "succeeded to write"
    except Exception as e:
        print(e)
        return "failed to write"
    finally:
        f.close()

@app.route('/lux', methods=['GET'])
def get_lux():
    try:
        f = open(file_path, 'r')
        for row in f:
            lux = row
    except Exception as e:
        print(e)
    finally:
        f.close()
        return lux

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = port_num)