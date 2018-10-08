package haha;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.DataInputStream;
import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;

@RestController
public class MyController {

    static ConcurrentHashMap<Integer, Integer> table = new ConcurrentHashMap<Integer, Integer>();

    static {
        DataInputStream cin = new DataInputStream(MyController.class.getResourceAsStream("/table.bin"));

        try {
            while (true) {
                int k = Integer.reverseBytes(cin.readInt()), v = Integer.reverseBytes(cin.readInt());
                table.put(k, v);
            }
        } catch (IOException e) {
        } finally {
            try {
                cin.close();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
        }
    }

    @RequestMapping("haha")
    static int getNextMove(int state) {
        return table.get(state);
    }
}
