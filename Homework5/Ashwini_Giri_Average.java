import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class Ashwini_Giri_Average{

    public static class TokenizerMapper extends Mapper<Object, Text, Text,Text>{
        
        private Text key_state = new Text();
        private Text value_val=new Text();
        
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] row = value.toString().split(",");
            String key_state1 = row[10].split(":")[1];
            key_state1 = key_state1.substring(0,key_state1.length()-1);
            int a=1;
            int var_age;
            String value_val1;
            value_val1 = row[1].split(":")[1]+","+Integer.toString(a);
            var_age=Integer.parseInt(row[4].split(":")[1]);
            if(var_age>=20 && var_age<=30){
                key_state.set(key_state1);
                value_val.set(value_val1);
                context.write(key_state, value_val);
            }
        }
    }

    public static class sumCalculate extends Reducer<Text,Text,Text,Text> {
        private Text result_val = new Text();

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            long summation = 0;
            long count=0;
            for (Text each_val : values) {
                String[] s= each_val.toString().split(",");
                summation+=Long.parseLong(s[0]);
                count+=Long.parseLong(s[1]);
            }
            String value=Long.toString(summation)+","+Long.toString(count);
            result_val.set(value);
            context.write(key, result_val);
        }
    }
    
    public static class sumToAverage extends Reducer<Text,Text,Text,FloatWritable> {
        private FloatWritable result_val = new FloatWritable();

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            long  summation = 0;
            long count=0;
            for (Text each_val : values) {
                String[] s= each_val.toString().split(",");
                summation+=Long.parseLong(s[0]);
                count+=Long.parseLong(s[1]);
            }
            float avg;
            avg=(float)summation/count;
            result_val.set(avg);
            context.write(key, result_val);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length < 2) {
            System.err.println("Usage: average <in> [<in>...] <out>");
            System.exit(2);
        }
        Job job = Job.getInstance(conf, "Average Sum");
        job.setJarByClass(Ashwini_Giri_Average.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(sumCalculate.class);
        job.setReducerClass(sumToAverage.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(FloatWritable.class);
        
        for (int i = 0; i < otherArgs.length - 1; ++i) {
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
        }
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[otherArgs.length - 1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

