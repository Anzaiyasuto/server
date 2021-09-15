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
    lux = str(lux)
    lux = float(lux)
    #print(type(lux))
    #print(1)

    temp = ''
    alpha = ''
    beta = ''
    theta = ''
    try:
        f = open(file_path, 'r')
        for row in f:
            alpha = row
            #print(alpha)
            #print(type(alpha)) ->str
        alpha = alpha.split(',')
        beta = alpha[1]
        theta = alpha[2]
    except Exception as e:
        print(e)
    finally:
        f.close()
    print('beta ' + beta)
    print('theta ' + theta)
    print('lux ' + lux)
    #print(" beta " + beta)
    #print(type(beta))
    beta = float(beta)
    #print(type(beta))
    
    #print(lux-beta)
    #print("temp " + temp )
    print("debug")
    if(math.fabs(lux-beta) < 50):
        temp = theta
    else:
        if(theta == flag[0]):
            temp = flag[1]
        else:
            temp = flag[0]    

    try:
        f = open(file_path, 'w')
        f.write(time + "," + lux + "," + temp)
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