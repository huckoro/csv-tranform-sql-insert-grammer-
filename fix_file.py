'''
   将数据文件转换成mysql的插入语句。暂时没有使用类封装
        数据源文件的数据必须为所有的字段，且和数据表创建时的顺序一致
        所得的结果存在在当前目录下的 result.txt 文件中

    notify:
        若源数据文件中的中文字段未加 '' 引号，可以使用，
        若已加 '' or "" 请搜索 TODO 获取解决

        数据源文件的 每一条记录之间不予许出现 空行 ，该条问题会在日后解决

        若记录使用',' or ';' etc.. 分隔，各字段的值会默认去掉前后空格,若不需要，请自行修改代码 line 57

'''
import time


# 不对下方列表中的字段串加 ''
default_list = ('default', 'null', '\'\'')  # 排除字符串


def get_key():
    ''' 获取文件名，分隔符，表名 '''
    file_name = input('请输入数据的源文件(需要在当前目录)：')
    delimiter = input('请输入分隔符：')
    table_name = input('请输入表名：')

    return file_name, delimiter, table_name


def parse_data(file_name, delimiter, table_name):
    ''' 处理数据 返回插入语句 '''
    res = 'insert into ' + str(table_name) + ' values \n'

    # 只读方式读取目标文件，将以' '空格分隔的数据转换成mysql插入语句
    with open(file_name, 'r') as f:
        while True:
            # 每次读取一行
            data = f.readline()
            if not data:
                break
            data_li = data.split(delimiter)

            # 删除换行 \n
            data_li[-1] = data_li[-1].replace('\n', '')
            try:
                while True:
                    data_li.remove('')
            except Exception as e:
                pass

            # TODO: 若字符已加 '' or "" 请注释掉下方 line 51 - 66 的代码，
            #  注:             日后会通过类的继承来解决这个问题
            # 对未加 '' 的字符添加
            data_list = list()
            for li in data_li:
                li = li.strip()
                if li.lower() not in default_list:
                    try:
                        int(li)
                    except ValueError:
                        li = '\'' + li + '\''
                        data_list.append(li)
                        continue
                # 若为数字
                data_list.append(li)

            # 调试
            # print(data_list)

            # 处理数据
            str_tmp = ','.join(data_list)
            # TODO: 若字符已加 '' or "" 请注释上一行代码，将下一行代码解除注释
            # str_tmp = ','.join(data_li)
            str_res = '(' + str_tmp + '),\n'
            res += str_res
            #  print(data_li)
            #  print(str_res)

    # print(res.rstrip(',\n'))
    res = res.rstrip(',\n')
    res += ';\n\n'

    return res


def save_data(res):
    ''' 将结果保存在当前目录下的 result.txt 中 '''
    date_time = time.strftime('  %Y-%m-%d & %H:%M:%S  ')
    s = '-'*20

    with open('./result.txt', 'a') as f:
        # 以追加的方式写入
        st = s + str(date_time) + s + '\n'
        f.write(st + res)


def main():
    ''' 主函数 '''
    # 获取关键参数
    file_name, delimiter, table_name = get_key()

    # 处理数据
    res = parse_data(file_name, delimiter, table_name)

    # 保存语句
    save_data(res)


if __name__ == '__main__':
    main()

